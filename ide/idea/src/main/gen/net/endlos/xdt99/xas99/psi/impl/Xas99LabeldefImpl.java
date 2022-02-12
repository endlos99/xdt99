// This is a generated file. Not intended for manual editing.
package net.endlos.xdt99.xas99.psi.impl;

import java.util.List;
import org.jetbrains.annotations.*;
import com.intellij.lang.ASTNode;
import com.intellij.psi.PsiElement;
import com.intellij.psi.PsiElementVisitor;
import com.intellij.psi.util.PsiTreeUtil;
import static net.endlos.xdt99.xas99.psi.Xas99Types.*;
import net.endlos.xdt99.xas99.psi.*;
import com.intellij.navigation.ItemPresentation;

public class Xas99LabeldefImpl extends Xas99NamedElementImpl implements Xas99Labeldef {

  public Xas99LabeldefImpl(@NotNull ASTNode node) {
    super(node);
  }

  public void accept(@NotNull Xas99Visitor visitor) {
    visitor.visitLabeldef(this);
  }

  @Override
  public void accept(@NotNull PsiElementVisitor visitor) {
    if (visitor instanceof Xas99Visitor) accept((Xas99Visitor)visitor);
    else super.accept(visitor);
  }

  @Override
  public String getName() {
    return Xas99PsiImplUtil.getName(this);
  }

  @Override
  public PsiElement setName(String newName) {
    return Xas99PsiImplUtil.setName(this, newName);
  }

  @Override
  public PsiElement getNameIdentifier() {
    return Xas99PsiImplUtil.getNameIdentifier(this);
  }

  @Override
  public ItemPresentation getPresentation() {
    return Xas99PsiImplUtil.getPresentation(this);
  }

}