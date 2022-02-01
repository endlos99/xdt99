// This is a generated file. Not intended for manual editing.
package net.endlos.xdt99.xas99r.psi.impl;

import java.util.List;
import org.jetbrains.annotations.*;
import com.intellij.lang.ASTNode;
import com.intellij.psi.PsiElement;
import com.intellij.psi.PsiElementVisitor;
import com.intellij.psi.util.PsiTreeUtil;
import static net.endlos.xdt99.xas99r.psi.Xas99RTypes.*;
import com.intellij.extapi.psi.ASTWrapperPsiElement;
import net.endlos.xdt99.xas99r.psi.*;

public class Xas99RInstructionImpl extends ASTWrapperPsiElement implements Xas99RInstruction {

  public Xas99RInstructionImpl(@NotNull ASTNode node) {
    super(node);
  }

  public void accept(@NotNull Xas99RVisitor visitor) {
    visitor.visitInstruction(this);
  }

  @Override
  public void accept(@NotNull PsiElementVisitor visitor) {
    if (visitor instanceof Xas99RVisitor) accept((Xas99RVisitor)visitor);
    else super.accept(visitor);
  }

  @Override
  @Nullable
  public Xas99RArgsI getArgsI() {
    return findChildByClass(Xas99RArgsI.class);
  }

  @Override
  @Nullable
  public Xas99RArgsII getArgsII() {
    return findChildByClass(Xas99RArgsII.class);
  }

  @Override
  @Nullable
  public Xas99RArgsIII getArgsIII() {
    return findChildByClass(Xas99RArgsIII.class);
  }

  @Override
  @Nullable
  public Xas99RArgsIV getArgsIV() {
    return findChildByClass(Xas99RArgsIV.class);
  }

  @Override
  @Nullable
  public Xas99RArgsIX getArgsIX() {
    return findChildByClass(Xas99RArgsIX.class);
  }

  @Override
  @Nullable
  public Xas99RArgsIXX getArgsIXX() {
    return findChildByClass(Xas99RArgsIXX.class);
  }

  @Override
  @Nullable
  public Xas99RArgsV getArgsV() {
    return findChildByClass(Xas99RArgsV.class);
  }

  @Override
  @Nullable
  public Xas99RArgsVI getArgsVI() {
    return findChildByClass(Xas99RArgsVI.class);
  }

  @Override
  @Nullable
  public Xas99RArgsVIII getArgsVIII() {
    return findChildByClass(Xas99RArgsVIII.class);
  }

  @Override
  @Nullable
  public Xas99RArgsVIIII getArgsVIIII() {
    return findChildByClass(Xas99RArgsVIIII.class);
  }

  @Override
  @Nullable
  public Xas99RArgsVIIIR getArgsVIIIR() {
    return findChildByClass(Xas99RArgsVIIIR.class);
  }

  @Override
  @Nullable
  public Xas99RArgsAdvI getArgsAdvI() {
    return findChildByClass(Xas99RArgsAdvI.class);
  }

  @Override
  @Nullable
  public Xas99RArgsAdvIV getArgsAdvIV() {
    return findChildByClass(Xas99RArgsAdvIV.class);
  }

  @Override
  @Nullable
  public Xas99RArgsAdvIa getArgsAdvIa() {
    return findChildByClass(Xas99RArgsAdvIa.class);
  }

  @Override
  @Nullable
  public Xas99RArgsAdvVI getArgsAdvVI() {
    return findChildByClass(Xas99RArgsAdvVI.class);
  }

  @Override
  @Nullable
  public Xas99RArgsAdvVIII getArgsAdvVIII() {
    return findChildByClass(Xas99RArgsAdvVIII.class);
  }

}
