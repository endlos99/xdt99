// This is a generated file. Not intended for manual editing.
package net.endlos.xdt99.xga99.psi.impl;

import java.util.List;
import org.jetbrains.annotations.*;
import com.intellij.lang.ASTNode;
import com.intellij.psi.PsiElement;
import com.intellij.psi.PsiElementVisitor;
import com.intellij.psi.util.PsiTreeUtil;
import static net.endlos.xdt99.xga99.psi.Xga99Types.*;
import com.intellij.extapi.psi.ASTWrapperPsiElement;
import net.endlos.xdt99.xga99.psi.*;
import com.intellij.psi.PsiReference;

public class Xga99OpLabelImpl extends ASTWrapperPsiElement implements Xga99OpLabel {

  public Xga99OpLabelImpl(@NotNull ASTNode node) {
    super(node);
  }

  public void accept(@NotNull Xga99Visitor visitor) {
    visitor.visitOpLabel(this);
  }

  @Override
  public void accept(@NotNull PsiElementVisitor visitor) {
    if (visitor instanceof Xga99Visitor) accept((Xga99Visitor)visitor);
    else super.accept(visitor);
  }

  @Override
  public String getName() {
    return Xga99PsiImplUtil.getName(this);
  }

  @Override
  public PsiElement setName(String newName) {
    return Xga99PsiImplUtil.setName(this, newName);
  }

  @Override
  public PsiElement getNameIdentifier() {
    return Xga99PsiImplUtil.getNameIdentifier(this);
  }

  @Override
  public PsiReference getReference() {
    return Xga99PsiImplUtil.getReference(this);
  }

}
